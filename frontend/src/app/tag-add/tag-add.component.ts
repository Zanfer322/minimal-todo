import { Component, OnInit } from '@angular/core';
import { TagAddService } from '../tag-add.service';

@Component({
  selector: 'app-tag-add',
  templateUrl: './tag-add.component.html',
  styleUrls: ['./tag-add.component.scss'],
})
export class TagAddComponent implements OnInit {
  visible: boolean;
  tag: string;
  choices: string[];

  constructor(private tagAdd: TagAddService) {}

  ngOnInit(): void {
    this.tagAdd.choices.subscribe((choices) => (this.choices = choices));
    this.tagAdd.active.subscribe((visible) => (this.visible = visible));
  }

  returnActiveTag() {
    if (this.tag == 'NN') {
      this.tagAdd.returnActiveTag(undefined);
      return;
    }
    this.tagAdd.returnActiveTag(this.tag);
    this.tag = undefined;
  }
}
