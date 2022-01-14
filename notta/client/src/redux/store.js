import { configureStore } from "@reduxjs/toolkit";
import logInFormSlice from "./form/logInFormSlice";
import registerFormSlice from "./form/registerFormSlice";

const store = configureStore({
    reducer: {
        logInForm: logInFormSlice.reducer,
        registerForm: registerFormSlice.reducer
    }
});

export default store;