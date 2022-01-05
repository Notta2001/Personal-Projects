import filtersReducer from '../components/Filters/FiltersSlice'
import todoListReducer from '../components/TodoList/TodosSlice'
import { combineReducers } from 'redux'

// const rootReducer = (state = {}, action) => {
//     // console.log(state, action)
//     return {
//         filters: filtersReducer(state.filters, action),
//         todoList: todoListReducer(state.todoList, action)
//     };
// };

const rootReducer = combineReducers({
    filters: filtersReducer,
    todoList: todoListReducer,
})

export default rootReducer