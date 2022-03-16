import { createSelector } from '@reduxjs/toolkit';

export const todoListSelector = (state) => state.todoList;
export const searchTextSelector = (state) => state.filters.search;
export const filterStatusSelector = (state) => state.filters.status;
export const filterPrioritiesSelector = (state) => state.filters.priority;

export const todosRemainingSelector = createSelector(
    todoListSelector, 
    searchTextSelector, 
    filterStatusSelector,
    filterPrioritiesSelector,
    (todoList, searchText, status, priorities) => {
        return todoList.filter((todo) => {
            if (status === 'All') { 
                return priorities.length 
                ? todo.name.includes(searchText) && priorities.includes(todo.priority)
                : todo.name.includes(searchText);
            }
            else {
                return todo.name.includes(searchText) && 
                (status === 'Completed' 
                ? todo.completed 
                : !todo.completed) && (priorities.length ? priorities.includes(todo.priority) : true);
            }
            
        });
    });
