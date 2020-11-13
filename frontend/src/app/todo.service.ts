import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Tag, Todo } from './models';
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
  private cachedTags?: Tag[];

  constructor(private http: HttpClient, private toast: ToastService) {
    this.cachedTags = undefined;
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

  private showErrorToast(res: ErrorRes) {
    console.error(res);
    let title = `${res.status} ${res.statusText}`;
    let message = `${res.url}\n\n${JSON.stringify(res.error, null, 2)}`;
    this.toast.addToast({ title, message, type: 'error' });
  }
}
