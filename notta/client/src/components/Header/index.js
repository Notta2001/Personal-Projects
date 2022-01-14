import React from 'react'
import { Box, Drawer, Button, List, Divider, ListItem, ListItemIcon, ListItemText, Typography } from '@mui/material';
import InboxIcon from '@mui/icons-material/MoveToInbox';
import MailIcon from '@mui/icons-material/Mail';
import { useState, useCallback } from 'react';
import { useStyles } from './styles';
import LogInForm from './LogInForm';
import RegisterForm from './RegisterForm';
import logInFormSlice from '../../redux/form/logInFormSlice';
import { useDispatch } from 'react-redux';

const Header = () => {
    const dispatch = useDispatch();
    const classes = useStyles();
    const [showDrawer, setShowDrawer] = useState(false);
    const anchor = 'left';

    const toggleDrawer = (anchor, open) => (event) => {
        if (event.type === 'keydown' && (event.key === 'Tab' || event.key === 'Shift')) {
          return;
        }
    
        setShowDrawer(open);
    };

    const openLogForm = useCallback(() => {
        dispatch(logInFormSlice.actions.showLogInForm());
    }, [dispatch]);

    const list = (anchor) => (
        <Box
          sx={{ width: 250 }}
          role="presentation"
          onClick={toggleDrawer(anchor, false)}
          onKeyDown={toggleDrawer(anchor, false)}
        >
          <List>
            {['Inbox', 'Starred', 'Send email', 'Drafts'].map((text, index) => (
              <ListItem button key={text}>
                <ListItemIcon>
                  {index % 2 === 0 ? <InboxIcon /> : <MailIcon />}
                </ListItemIcon>
                <ListItemText primary={text} />
              </ListItem>
            ))}
          </List>
          <Divider />
          <List>
            {['All mail', 'Trash', 'Spam'].map((text, index) => (
              <ListItem button key={text}>
                <ListItemIcon>
                  {index % 2 === 0 ? <InboxIcon /> : <MailIcon />}
                </ListItemIcon>
                <ListItemText primary={text} />
              </ListItem>
            ))}
          </List>
        </Box>
      );

    return (
        <Box className={classes.container} >
            <React.Fragment key={anchor}>
                <Button className={classes.drawer} onClick={toggleDrawer(anchor, true)}>MENU</Button>
                <Drawer
                    anchor={anchor}
                    open={showDrawer}
                    onClose={toggleDrawer(anchor, false)}
                >
                    {list(anchor)}
                </Drawer>
            </React.Fragment>
            <Typography variant="h2" align='center' className={classes.mainText}>BLOG</Typography>
            <LogInForm />
            <RegisterForm/>
            <Button variant="outlined" className={classes.logInButton}onClick={openLogForm}>Log In</Button>
        </Box>
    )
}

export default Header;
