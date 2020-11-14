import {
  AfterViewInit,
  Component,
  ElementRef,
  Input,
  OnInit,
  ViewChild,
} from '@angular/core';
import { Todo } from '../models';
import { ToastService } from '../toast.service';
import { TodoService } from '../todo.service';

@Component({
  selector: 'app-todo',
  templateUrl: './todo.component.html',
  styleUrls: ['./todo.component.scss'],
})
export class TodoComponent implements OnInit, AfterViewInit {
  @Input() todo: Todo;

  @ViewChild('todoContent') todoContent: ElementRef<HTMLDivElement>;

  constructor(private todoService: TodoService, private toast: ToastService) {}

  ngOnInit(): void {}

  ngAfterViewInit(): void {
    this.todoContent.nativeElement.textContent = this.todo.contents;
  }

  async toggleChecked() {
    if (this.todo.state == 'cancelled') {
      return;
    }

    if (this.todo.state == 'done') {
      this.todo.state = 'ongoing';
    } else if (this.todo.state == 'ongoing') {
      this.todo.state = 'done';
    }
    await this.updateTodo();
  }

  async toggleBin() {
    if (this.todo.state == 'cancelled') {
      this.todo.state = 'ongoing';
    } else {
      this.todo.state = 'cancelled';
    }
    await this.updateTodo();
  }

  async contentFocusLost() {
    let newContent = this.todoContent.nativeElement.textContent;
    if (this.todo.contents == newContent) {
      return;
    }
    this.todo.contents = newContent;
    await this.updateTodo();

    this.toast.addToast({
      type: 'info',
      title: 'Focus lost',
      message: this.todoContent.nativeElement.textContent,
    });
  }

  private async updateTodo() {
    let todo = await this.todoService.updateTodo({
      id: this.todo.id,
      contents: this.todo.contents,
      state: this.todo.state,
      tags: this.todo.tags,
    });
    if (todo == null) {
      return;
    }
    this.todo = todo;
    this.todoContent.nativeElement.textContent = todo.contents;

    this.toast.addToast({
      type: 'info',
      title: 'Updated Todo',
      message: 'Updated todo',
    });
  }
}
