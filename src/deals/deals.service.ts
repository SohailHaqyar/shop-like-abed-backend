import { Injectable } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { getManager, Repository } from 'typeorm';
import { AddDealDto } from './add-deals.dto';
import { Deal } from './entities/deal.entity';

@Injectable()
export class DealsService {
  constructor(
    @InjectRepository(Deal)
    private dealsRepository: Repository<Deal>,
  ) {}

  async getDeals() {
    return await this.dealsRepository.findAndCount();
  }

  async getDeal(id: string) {
    return await this.dealsRepository.findOne(id);
  }

  async addDeal(addDealDto: AddDealDto) {
    const deal = this.dealsRepository.create(addDealDto);
    return await this.dealsRepository.save(deal);
  }

  async bulkAddDeals(deals: AddDealDto[]) {
    let requests = [];
    deals.map((deal) => {
      requests.push(
        this.dealsRepository.save(this.dealsRepository.create(deal)),
      );
    });
    return await Promise.all(requests);
  }

  async nuke() {
    const deals = await this.dealsRepository.find();
    const result = await getManager().transaction(async (entityManager) => {
      await entityManager.delete(
        Deal,
        deals.map((entity) => entity.id),
      );
    });
    return result;
  }

  async updateDeal(id: string, updateDealDto: AddDealDto) {
    const deal = await this.dealsRepository.findOne(id);
    Object.assign(deal, updateDealDto);
    return await this.dealsRepository.save(deal);
  }
}
