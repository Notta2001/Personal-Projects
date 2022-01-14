import React from 'react';
import { Button, Modal, TextField, Typography } from '@mui/material'
import { useCallback, useState } from 'react';
import logInFormSlice from '../../../redux/form/logInFormSlice';
import registerFormSlice from '../../../redux/form/registerFormSlice'
import useStyles from './styles';
import {useDispatch, useSelector} from 'react-redux';
import { sha256 } from 'js-sha256';
import * as api from '../../../api'
import axios from 'axios';

const LogInForm = () => {
    const classes = useStyles();

    const [account, setAccount] = useState({
        userName: '',
        password: ''
    });

    const dispatch = useDispatch();
    const { isShow } = useSelector(state => state.logInForm);

    const onClose = useCallback(() => {
        dispatch(logInFormSlice.actions.hideLogInForm());
        setAccount({
          userName: '',
          password: ''
        });
      }, [dispatch]);

    const handleLogIn = (async () => {
      try{
        console.log(account.userName)
        const curAccount = await axios.post(`http://localhost:5000/account/logIn`, {userName: account.userName});
        if (sha256(account.password) === curAccount.data[0].password) {
          alert('Log In Successful!')
          dispatch(logInFormSlice.actions.hideLogInForm());
          setAccount({
            userName: '',
            password: ''
          });
        } else {
          alert('Wrong username or password!')
        }
      } catch (err) {
        alert('Wrong username or password!')
        console.log(err);
      }
      
    });

    const handleChangeRegister = useCallback(() => {
      dispatch(logInFormSlice.actions.hideLogInForm());
      dispatch(registerFormSlice.actions.showRegisterForm());
    }, [dispatch]);  

    const body = (
        <div className={classes.paper} id='simple-modal-title'>
          <h2>Welcome to TD Blog App!</h2>
          <Typography variant="h7" style={{marginBottom: '10px'}}>Please sign in to use</Typography>
          <form noValidate autoComplete='off' className={classes.form}>
            <TextField
              className={classes.title}
              required
              label='User Name'
              value={account.userName}
              placeholder='Username...'
              onChange={(e) => {
                setAccount({ ...account, userName: e.target.value });
                console.log(e.target.value)}}
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
                onClick={handleLogIn}
              >
                Log In
              </Button>
              <Button
                variant='contained'
                color='primary'
                component='span'
                onClick={handleChangeRegister}
              >
                Register
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

export default LogInForm
