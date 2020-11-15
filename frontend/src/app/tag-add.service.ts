import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class TagAddService {
  active: BehaviorSubject<boolean>;
  cb?: (tag: string) => void;
  choices?: BehaviorSubject<string[]>;

  constructor() {
    this.active = new BehaviorSubject<boolean>(false);
    this.choices = new BehaviorSubject<string[]>([]);
  }

  getTagToAdd(
    choices: string[] | undefined,
    cb: (tag: string) => void
  ): string {
    if (this.active.value == true) {
      console.log('already active');
      return undefined;
    }
    this.cb = cb;
    this.choices.next(choices);
    this.active.next(true);
  }

  returnActiveTag(tag: string) {
    if (this.active.value == false) {
      return;
    }

    this.cb(tag);

    this.active.next(false);
    this.cb = undefined;
    this.choices.next([]);
  }
}
