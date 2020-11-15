import { Component, HostListener, OnInit, Renderer2 } from '@angular/core';
import { Todo } from '../models';
import { TodoService } from '../todo.service';

@Component({
  selector: 'app-todo-list',
  templateUrl: './todo-list.component.html',
  styleUrls: ['./todo-list.component.scss'],
})
export class TodoListComponent implements OnInit {
  todoList: Todo[];

  constructor(private todoService: TodoService) {}

  async ngOnInit(): Promise<void> {
    this.todoList = await this.todoService.getAllTodo();
  }

  async createTodo(): Promise<void> {
    let todo = await this.todoService.createTodo({ contents: '', tags: [] });
    this.todoList.push(todo);
  }

  handleKeyboard() {
    console.log('Got keyboard event');
  }
}
