import React from 'react';
import { Button, Modal, TextField, Typography } from '@mui/material'
import { useCallback, useState } from 'react';
import registerFormSlice from '../../../redux/form/registerFormSlice';
import useStyles from './styles';
import {useDispatch, useSelector} from 'react-redux';
import logInFormSlice from '../../../redux/form/logInFormSlice';
import { sha256 } from 'js-sha256';
import axios from 'axios';

const RegisterForm = () => {
    const classes = useStyles();

    const [account, setAccount] = useState({
        name: '',
        userName: '',
        password: ''
    });

    const dispatch = useDispatch();
    const { isShow } = useSelector(state => state.registerForm);

    const onClose = useCallback(() => {
        dispatch(registerFormSlice.actions.hideRegisterForm());
        setAccount({
          name: '',
          userName: '',
          password: ''
        });
      }, [dispatch]);

    const handleRegister = (async () => {
      try{
        await axios.post(`http://localhost:5000/account`, {
          name: account.name,
          userName: account.userName,
          password: sha256(account.password)
        });
        alert('Register successful!!')
        dispatch(registerFormSlice.actions.hideRegisterForm());
        setAccount({
          name: '',
          userName: '',
          password: ''
        });
      } catch (err) {
        alert('Wrong username or password!')
        console.log(err);
      }
    });

    const handleChangLogIn = (() => {
      dispatch(registerFormSlice.actions.hideRegisterForm());
      dispatch(logInFormSlice.actions.showLogInForm());
    })

    const body = (
        <div className={classes.paper} id='simple-modal-title'>
          <h2>Please fill in the form!</h2>
          <form noValidate autoComplete='off' className={classes.form}>
            <TextField
              className={classes.title}
              required
              label='Name'
              value={account.name}
              placeholder='Username...'
              onChange={(e) => setAccount({ ...account, name: e.target.value })}
            />
            <TextField
              className={classes.title}
              required
              label='User Name'
              value={account.userName}
              placeholder='Username...'
              onChange={(e) => setAccount({ ...account, userName: e.target.value })}
            />
            <TextField
              className={classes.title}
              required
              label='Password'
              type='password'
              value={account.password}
              placeholder='Password...'
              onChange={(e) => setAccount({ ...account, password: e.target.value})}
            />
            <div className={classes.footer}>
              <Button
                variant='contained'
                color='primary'
                component='span'
                onClick={handleRegister}
              >
                Register
              </Button>
              <Button
                variant='contained'
                color='primary'
                component='span'
                onClick={handleChangLogIn}
              >
                Log In
              </Button>
            </div>
          </form>
        </div>
      );

    return (
        <Modal open={isShow} onClose={onClose}>
            {body}
        </Modal>
    )
}

export default RegisterForm
