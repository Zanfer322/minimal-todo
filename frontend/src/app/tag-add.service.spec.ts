import { TestBed } from '@angular/core/testing';

import { TagAddService } from './tag-add.service';

describe('TagAddService', () => {
  let service: TagAddService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(TagAddService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
