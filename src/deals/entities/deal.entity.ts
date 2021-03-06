import { Column, Entity, PrimaryGeneratedColumn } from 'typeorm';
import { CreatableEntity } from '../../classes/creatables';
import { SupermarketSource } from '../add-deals.dto';

@Entity()
export class Deal extends CreatableEntity {
  @PrimaryGeneratedColumn('uuid')
  id: string;

  @Column()
  title: string;

  @Column()
  link: string;

  @Column()
  image_url: string;

  @Column()
  old_price: string;

  @Column()
  new_price: string;

  @Column()
  discount_details: string;
  
  @Column()
  label: string;


  @Column()
  source: SupermarketSource;
}
