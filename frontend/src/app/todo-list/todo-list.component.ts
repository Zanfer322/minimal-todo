import { Component, HostListener, OnInit, Renderer2 } from '@angular/core';
import { Todo } from '../models';
import { TagAddService } from '../tag-add.service';
import { TodoFilterService } from '../todo-filter.service';
import { TodoService } from '../todo.service';

@Component({
  selector: 'app-todo-list',
  templateUrl: './todo-list.component.html',
  styleUrls: ['./todo-list.component.scss'],
})
export class TodoListComponent implements OnInit {
  todoList: Todo[];
  tags: string[];
  activeTags: string[];
  searchTerm: string;

  constructor(
    private todoService: TodoService,
    private todoFilter: TodoFilterService,
    private tagAddService: TagAddService
  ) {}

  async ngOnInit(): Promise<void> {
    this.todoFilter.todoList.subscribe(
      (todoList) => (this.todoList = todoList)
    );
    this.todoService.tags.subscribe((tags) => (this.tags = tags));
    this.activeTags = [];
  }

  async createTodo(): Promise<void> {
    let todo = await this.todoService.createTodo({ contents: '', tags: [] });
    this.todoList.push(todo);
  }

  async updateSearch() {
    console.log(this.searchTerm);
    if (this.searchTerm == null || this.searchTerm == '') {
      await this.todoFilter.setSearchTerm(undefined);
    } else {
      await this.todoFilter.setSearchTerm(this.searchTerm);
    }
  }

  async toggleTag(tag: string) {
    let index = this.activeTags.indexOf(tag);
    if (index == -1) {
      this.activeTags.push(tag);
    } else {
      this.activeTags.splice(index, 1);
    }
    console.log(this.activeTags);
    await this.todoFilter.setTags(this.activeTags);
  }

  async addTag() {
    this.tagAddService.getTagToAdd(undefined, (tag) => {
      if (tag == null || tag == '') {
        return;
      }
      this.todoService.createTag(tag);
    });
  }
}
