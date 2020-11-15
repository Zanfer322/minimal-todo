import { Injectable } from '@angular/core';
import { Toast } from './models';

@Injectable({
  providedIn: 'root',
})
export class ToastService {
  toasts: Toast[];

  constructor() {
    this.toasts = [];
  }

  addToast(toast: Toast) {
    this.toasts.push(toast);
  }

  removeToast(index: number) {
    this.toasts.splice(index, 1);
  }
}
