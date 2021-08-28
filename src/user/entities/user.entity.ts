import { Column, Entity, PrimaryGeneratedColumn } from 'typeorm';
import { CreatableEntity } from '../../classes/creatables';

@Entity()
export class User extends CreatableEntity {
  @PrimaryGeneratedColumn('uuid')
  id: string;

  @Column({ nullable: true })
  password: string;

  @Column()
  avatar: string;

  @Column()
  email: string;

  @Column()
  full_name: string;
}
