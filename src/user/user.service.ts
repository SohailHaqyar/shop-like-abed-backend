import { BadRequestException, Injectable } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { tryCatch } from 'src/helpers/try-catch';
import { getManager, Repository } from 'typeorm';
import { CreateUserDto } from './dtos/create-user.dto';
import { User } from './entities/user.entity';
import { hash } from 'bcrypt';
import { OAuth2Client } from 'google-auth-library';
import { GOOGLE_CLIENT_ID } from 'src/helpers/constants';
import { JwtService } from '@nestjs/jwt';

@Injectable()
export class UserService {
  constructor(
    @InjectRepository(User)
    private userRepository: Repository<User>,
    private jwtService: JwtService,
  ) {}

  // find all users
  async findAll() {
    return await this.userRepository.findAndCount();
  }
  // find user by id
  async findOne(id: string): Promise<User> {
    const [data, error] = await tryCatch(this.userRepository.findOne(id));
    error && this.throwError();
    error && console.error(error);
    return data;
  }

  // create a user with createUserDto
  async createUser(createUserDto: CreateUserDto): Promise<User> {
    const seed = createUserDto.full_name + createUserDto.email;
    createUserDto.password = await this.hashPassword(createUserDto.password);

    createUserDto.avatar = this.generateAvatar(
      seed.replace(' ', '').toLowerCase(),
    );
    const [user, error] = await tryCatch(
      this.userRepository.save(this.userRepository.create(createUserDto)),
    );
    error && this.throwError();
    error && console.error(error);
    return user;
  }

  generateAvatar(seed: string) {
    return `https://avatars.dicebear.com/api/bottts/${seed}.svg`;
  }

  // hash passowrd with bcrypt
  async hashPassword(password: string) {
    return await hash(password, 8);
  }

  async throwError(): Promise<void> {
    throw new BadRequestException('Bad Request');
  }

  async nuke() {
    const deals = await this.userRepository.find();
    const result = await getManager().transaction(async (entityManager) => {
      await entityManager.delete(
        User,
        deals.map((entity) => entity.id),
      );
    });
    return result;
  }

  async findUserByEmail(email: string) {
    const user = await this.userRepository.findOne({
      where: {
        email,
      },
    });
    return !user ? null : user;
  }

  async verifyGoogleToken(idToken: string) {
    const client = new OAuth2Client(GOOGLE_CLIENT_ID);
    const ticket = await client.verifyIdToken({ idToken });
    return ticket.getPayload();
  }

  async genjwt(payload: any) {
    return {
      access_token: this.jwtService.sign(payload),
    };
  }
  async continueWithGoogle(googleIdToken: string) {
    const result = await this.verifyGoogleToken(googleIdToken);
    const avatar = this.generateAvatar(
      (result.email + result.name).replace(' ', ''),
    );
    const user = await this.findUserByEmail(result.email);
    if (!user) {
      const createdUser = await this.userRepository.save(
        this.userRepository.create({
          email: result.email,
          full_name: result.name,
          avatar,
        }),
      );
      const payload = { sub: createdUser.id, email: createdUser.email };
      return this.genjwt(payload);
    }
    const payload = { sub: user.id, email: user.email };
    return this.genjwt(payload);
  }
}
