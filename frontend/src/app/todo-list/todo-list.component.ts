import { Component, HostListener, OnInit, Renderer2 } from '@angular/core';
import { Todo } from '../models';
import { TodoFilterService } from '../todo-filter.service';
import { TodoService } from '../todo.service';

@Component({
  selector: 'app-todo-list',
  templateUrl: './todo-list.component.html',
  styleUrls: ['./todo-list.component.scss'],
})
export class TodoListComponent implements OnInit {
  todoList: Todo[];
  searchTerm: string;

  constructor(
    private todoService: TodoService,
    private todoFilter: TodoFilterService
  ) {}

  async ngOnInit(): Promise<void> {
    this.todoFilter.todoList.subscribe(
      (todoList) => (this.todoList = todoList)
    );
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
}
