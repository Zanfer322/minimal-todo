import { TestBed } from '@angular/core/testing';

import { TodoFilterService } from './todo-filter.service';

describe('TodoFilterService', () => {
  let service: TodoFilterService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(TodoFilterService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
