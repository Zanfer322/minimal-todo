import { Component, HostListener, OnInit, Renderer2 } from '@angular/core';
import { Todo, TodoState } from '../models';
import { TagAddService } from '../tag-add.service';
import { TodoFilterService } from '../todo-filter.service';
import { TodoService } from '../todo.service';

interface TodoBunch {
  day: string;
  todoList: Todo[];
}

@Component({
  selector: 'app-todo-list',
  templateUrl: './todo-list.component.html',
  styleUrls: ['./todo-list.component.scss'],
})
export class TodoListComponent implements OnInit {
  todoBunches: TodoBunch[];
  todoList: Todo[];
  tags: string[];
  activeTags: string[];
  searchTerm: string;

  states: TodoState[];
  activeStates: TodoState[];

  constructor(
    private todoService: TodoService,
    private todoFilter: TodoFilterService,
    private tagAddService: TagAddService
  ) {}

  async ngOnInit(): Promise<void> {
    this.todoBunches = [];
    this.todoFilter.todoList.subscribe((todoList) => {
      this.todoList = todoList;
      this.todoBunches = this.bunchTodo(todoList);
    });
    this.todoService.tags.subscribe((tags) => (this.tags = tags));
    this.activeTags = [];
    this.states = ['ongoing', 'done', 'cancelled'];
    this.activeStates = [];
  }

  private bunchTodo(todoList: Todo[]): TodoBunch[] {
    let bunches: TodoBunch[] = [];
    todoList = todoList.sort(
      (a, b) => a.createdAt.getTime() - b.createdAt.getTime()
    );

    let curBunch: TodoBunch = null;
    for (let todo of todoList) {
      let day = todo.createdAt.toLocaleDateString(undefined, {
        day: 'numeric',
        month: 'short',
        weekday: 'short',
      });
      if (curBunch == null) {
        curBunch = {
          day: day,
          todoList: [todo],
        };
        continue;
      }
      if (curBunch.day == day) {
        curBunch.todoList.push(todo);
        continue;
      }
      bunches.push(curBunch);

      curBunch = {
        day: day,
        todoList: [todo],
      };
    }
    bunches.push(curBunch);

    return bunches;
  }

  async createTodo(): Promise<void> {
    let todo = await this.todoService.createTodo({ contents: '', tags: [] });
    this.todoList.push(todo);
    this.todoBunches = this.bunchTodo(this.todoList);
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

  async toggleState(state: TodoState) {
    let index = this.activeStates.indexOf(state);
    if (index == -1) {
      this.activeStates.push(state);
    } else {
      this.activeStates.splice(index, 1);
    }
    await this.todoFilter.setState(this.activeStates);
  }
}
