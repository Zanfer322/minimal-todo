import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';
import { FilterTodo, Todo, TodoState } from './models';
import { TodoService } from './todo.service';

@Injectable({
  providedIn: 'root',
})
export class TodoFilterService {
  tags?: string[];
  searchTerm?: string;
  state?: TodoState;

  todoList: BehaviorSubject<Todo[]>;

  constructor(private todoService: TodoService) {
    this.todoList = new BehaviorSubject<Todo[]>([]);
    this.updateTodoList();
  }

  async addTag(tag: string) {
    if (this.tags == null) {
      this.tags = [tag];
    } else if (this.tags.includes(tag)) {
      return;
    }
    this.tags.push(tag);
    await this.updateTodoList();
  }

  async removeTag(tag: string) {
    if (this.tags == null) {
      return;
    }

    let index = this.tags.indexOf(tag);
    if (index == -1) {
      return;
    }
    this.tags.splice(index, 1);
    if (this.tags.length == 0) {
      this.tags = undefined;
    }
    await this.updateTodoList();
  }

  async setTags(tags: string[]) {
    if (tags.length == 0) {
      this.tags == undefined;
    } else {
      this.tags = tags;
    }
    await this.updateTodoList();
  }

  async setState(state?: TodoState) {
    this.state = state;
    await this.updateTodoList();
  }

  async setSearchTerm(searchTerm?: string) {
    this.searchTerm = searchTerm;
    await this.updateTodoList();
  }

  private async updateTodoList() {
    if (this.searchTerm != null) {
      let todoList = await this.todoService.searchTodo({
        searchTerm: this.searchTerm,
      });
      if (this.state != null) {
        todoList = todoList.filter((todo) => todo.state == this.state);
      }
      if (this.tags != null) {
        todoList = todoList.filter((todo) => {
          for (let tag of this.tags) {
            if (!todo.tags.includes(tag)) {
              return false;
            }
          }
          return true;
        });
      }
      this.todoList.next(todoList);
      return;
    }

    let filter: FilterTodo = {
      tags: this.tags,
      state: this.state,
    };
    console.log(filter);
    let todoList = await this.todoService.getAllTodo(filter);
    this.todoList.next(todoList);
  }
}
