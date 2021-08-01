import { Module } from '@nestjs/common';
import { TypeOrmModule } from '@nestjs/typeorm';
import { AppController } from './app.controller';
import { AppService } from './app.service';
import { DealsModule } from './deals/deals.module';
import { Deal } from './deals/entities/deal.entity';

@Module({
  imports: [
    TypeOrmModule.forRoot({
      type: 'postgres',
      url: 'postgres://ujbrkebwzxtcwn:f17578aad6cb2f0bacd7c387242c4d5199f23de4699421a0a7115c4ef6716bbb@ec2-54-155-254-112.eu-west-1.compute.amazonaws.com:5432/dac2to4fbdpmqc',
      entities: [Deal],
      ssl: {
        rejectUnauthorized: false,
      },
      synchronize: true,
      logging: false,
      retryAttempts: 1,
    }),
    DealsModule,
  ],
  controllers: [AppController],
  providers: [AppService],
})
export class AppModule {}
