import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Tag, Todo } from './models';

@Injectable({
  providedIn: 'root',
})
export class TodoService {
  private cachedTags?: Tag[];

  constructor(private http: HttpClient) {
    this.cachedTags = undefined;
  }

  async createTag(name: string): Promise<Tag> {
    let data = await this.http.post('/api/tags/', { name }).toPromise();
    let tag = this.toTag(data);
    if (this.cachedTags) {
      this.cachedTags.push(tag);
    }
    return tag;
  }

  async getAllTags(refresh: boolean = false): Promise<Tag[]> {
    if (refresh == true && this.cachedTags != null) {
      return this.cachedTags;
    }
    let dataArr = await this.http.get<any[]>('/api/tags/').toPromise();
    let tags = dataArr.map((data) => this.toTag(data));
    this.cachedTags = tags;
    return tags;
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
}
