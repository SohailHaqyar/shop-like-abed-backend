import { Body, Controller, Delete, Get, Post } from '@nestjs/common';
import { AddDealDto } from './add-deals.dto';

import { DealsService } from './deals.service';

@Controller('deals')
export class DealsController {
  constructor(private readonly dealsService: DealsService) {}

  @Get()
  getData() {
    return this.dealsService.getDeals();
  }

  @Post()
  addDeal(@Body() addDealDto: AddDealDto) {
    return this.dealsService.addDeal(addDealDto);
  }

  @Post('/bulk')
  bulkAddDeals(@Body() multiplAddDealDtos: AddDealDto[]) {
    return this.dealsService.bulkAddDeals(multiplAddDealDtos);
  }

  @Delete('/nuke')
  nuke() {
    return this.dealsService.nuke();
  }
}
