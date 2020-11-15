import {
  HttpClient,
  HttpParams,
  HTTP_INTERCEPTORS,
} from '@angular/common/http';
import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';
import {
  CreateTodo,
  FilterTodo,
  SearchTodo,
  Tag,
  Todo,
  UpdateTodo,
} from './models';
import { ToastService } from './toast.service';

interface ErrorRes {
  status: number;
  statusText: string;
  url: string;
  error: any;
}

@Injectable({
  providedIn: 'root',
})
export class TodoService {
  tags: BehaviorSubject<string[]>;
  private cachedTags?: Tag[];

  constructor(private http: HttpClient, private toast: ToastService) {
    this.cachedTags = undefined;
    this.tags = new BehaviorSubject<string[]>([]);
    this.getAllTags();
  }

  async createTag(name: string): Promise<Tag | undefined> {
    try {
      var data = await this.http.post('/api/tags/', { name }).toPromise();
    } catch (e) {
      this.showErrorToast(e);
      return undefined;
    }

    let tag = this.toTag(data);
    if (this.cachedTags) {
      this.cachedTags.push(tag);
      this.tags.next(this.cachedTags.map((tag) => tag.name));
    }
    return tag;
  }

  async getAllTags(refresh: boolean = false): Promise<Tag[] | undefined> {
    if (refresh == true && this.cachedTags != null) {
      return this.cachedTags;
    }

    try {
      var dataArr = await this.http.get<any[]>('/api/tags/').toPromise();
    } catch (e) {
      this.showErrorToast(e);
      return undefined;
    }

    let tags = dataArr.map((data) => this.toTag(data));
    this.cachedTags = tags;
    this.tags.next(this.cachedTags.map((tag) => tag.name));
    return tags;
  }

  async createTodo(createTodo: CreateTodo): Promise<Todo | undefined> {
    try {
      var data = await this.http.post('/api/todo/', createTodo).toPromise();
    } catch (e) {
      this.showErrorToast(e);
      return undefined;
    }

    let todo = this.toTodo(data);
    return todo;
  }

  async getAllTodo(filter?: FilterTodo): Promise<Todo[] | undefined> {
    let params: HttpParams;
    if (filter == null) {
      params = new HttpParams();
    } else {
      params = this.toFilterParams(filter);
    }
    console.log(params);

    try {
      var dataArr = await this.http
        .get<any[]>('/api/todo', { params })
        .toPromise();
    } catch (e) {
      this.showErrorToast(e);
      return undefined;
    }
    let todo = dataArr.map((data) => this.toTodo(data));
    return todo;
  }

  async searchTodo(searchTodo: SearchTodo): Promise<Todo[] | undefined> {
    let params = this.toSearchParams(searchTodo);
    try {
      var dataArr = await this.http
        .get<any[]>('/api/todo/search', { params })
        .toPromise();
    } catch (e) {
      this.showErrorToast(e);
      return undefined;
    }

    let todo = dataArr.map((data) => this.toTodo(data));
    return todo;
  }

  async updateTodo(updateTodo: UpdateTodo): Promise<Todo | undefined> {
    try {
      var data = await this.http.put('/api/todo/', updateTodo).toPromise();
    } catch (e) {
      this.showErrorToast(e);
      return undefined;
    }

    let todo = this.toTodo(data);
    return todo;
  }

  private toTag(data: any): Tag {
    return {
      id: data.id,
      name: data.name,
      createdAt: new Date(data['created_at']),
    };
  }

  private toTodo(data: any): Todo {
    return {
      id: data.id,
      contents: data.contents,
      state: data.state,
      tags: data.tags,
      createdAt: new Date(data['created_at']),
      updatedAt: new Date(data['updated_at']),
      stateUpdatedAt: new Date(data['state_updated_at']),
    };
  }

  private toFilterParams(filter: FilterTodo): HttpParams {
    let params = new HttpParams();
    if (filter.state != null) {
      params = params.set('state', filter.state);
    }
    if (filter.startTime != null) {
      params = params.set('start_time', filter.startTime.toISOString());
    }
    if (filter.endTime != null) {
      params = params.set('end_time', filter.endTime.toISOString());
    }
    if (filter.tags != null) {
      for (let tag of filter.tags) {
        params = params.append('tags', tag);
      }
    }
    if (filter.limit != null) {
      params = params.set('limit', filter.limit.toString());
    }
    if (filter.offset != null) {
      params = params.set('offset', filter.offset.toString());
    }
    return params;
  }

  private toSearchParams(search: SearchTodo): HttpParams {
    let params = new HttpParams();
    if (search.searchTerm != null) {
      params = params.set('search_term', search.searchTerm);
    }
    if (search.limit != null) {
      params = params.set('limit', search.limit.toString());
    }
    if (search.offset != null) {
      params = params.set('offset', search.offset.toString());
    }
    return params;
  }

  private showErrorToast(res: ErrorRes) {
    console.error(res);
    let title = `${res.status} ${res.statusText}`;
    let message = `${res.url}\n\n${JSON.stringify(res.error, null, 2)}`;
    this.toast.addToast({ title, message, type: 'error' });
  }
}
