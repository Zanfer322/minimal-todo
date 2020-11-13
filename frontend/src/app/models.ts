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

export interface FilterTodo {
  state?: TodoState;
  startTime?: Date;
  endTime?: Date;
  tags?: string[];
  limit?: number;
  offset?: number;
}

export interface Tag {
  id: string;
  name: string;
  createdAt: Date;
}

export interface Toast {
  title: string;
  message: string;
  type: 'info' | 'success' | 'error';
}
