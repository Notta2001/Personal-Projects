import { createSlice } from "@reduxjs/toolkit";

export default createSlice({
    name: 'logInForm',
    initialState: {
        isShow: false
    },
    reducers: {
        showLogInForm: (state, action) => {
            state.isShow = true;
        },
        hideLogInForm: (state, action) => {
            state.isShow = false;
        }
    }
})