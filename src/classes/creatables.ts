import { CreateDateColumn, UpdateDateColumn } from 'typeorm';

export abstract class CreatableEntity {
  @CreateDateColumn()
  created_at: Date;

  @UpdateDateColumn()
  updated_at: Date;
}
