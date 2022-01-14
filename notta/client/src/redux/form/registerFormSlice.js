import { createSlice } from "@reduxjs/toolkit";

export default createSlice({
    name: 'registerForm',
    initialState: {
        isShow: false
    },
    reducers: {
        showRegisterForm: (state, action) => {
            state.isShow = true;
        },
        hideRegisterForm: (state, action) => {
            state.isShow = false;
        }
    }
})