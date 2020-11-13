import { Component, OnInit } from '@angular/core';
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

  async createTag() {
    let todo = await this.todoService.createTodo({
      contents: 'todo contents',
      tags: ['tag 1', 'tag 2'],
    });

    // console.log(todo);

    // let todoList = await this.todoService.getAllTodo();
    // console.log(todoList);
  }
}
