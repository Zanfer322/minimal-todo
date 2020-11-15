import { Component, OnInit } from '@angular/core';
import { Toast } from '../models';
import { ToastService } from '../toast.service';

@Component({
  selector: 'app-toast',
  templateUrl: './toast.component.html',
  styleUrls: ['./toast.component.scss'],
})
export class ToastComponent implements OnInit {
  toasts: Toast[];

  constructor(private toastService: ToastService) {}

  ngOnInit(): void {
    this.toasts = this.toastService.toasts;
  }

  removeToast(index: number) {
    this.toastService.removeToast(index);
  }
}
