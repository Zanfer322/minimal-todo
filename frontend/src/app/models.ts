export type TodoState = 'ongoing' | 'done' | 'cancelled';

export interface Todo {
  id: string;
  contents: string;
  state: TodoState;
  tags: string[];
  createdAt: Date;
  updatedAt: Date;
  stateUpdatedAt: Date;
}

export interface CreateTodo {
  contents: string;
  tags: string[];
}

export interface UpdateTodo {
  id: string;
  contents: string;
  state: TodoState;
  tags: string[];
}

export interface Tag {
  id: string;
  name: string;
  createdAt: Date;
}
