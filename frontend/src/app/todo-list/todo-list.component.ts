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
    // await this.todoService.createTag('fly');
    // await this.todoService.createTag('SapComponent');
    // let todo = await this.todoService.createTodo({
    //   contents: 'This one has many tags',
    //   tags: [],
    // });
    // await this.todoService.updateTodo({
    //   id: 'de2d619bd8f6475aa40c7f9c0a469ebd',
    //   contents: 'Do something quickly. This has no tags.',
    //   tags: [],
    //   state: 'cancelled',
    // });
    // console.log(todo);
    // let todoList = await this.todoService.getAllTodo();
    // console.log(todoList);
  }
}
