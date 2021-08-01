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
      host: 'localhost',
      port: 5432,
      username: 'root',
      password: 'root',
      database: 'db',
      entities: [Deal],
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
