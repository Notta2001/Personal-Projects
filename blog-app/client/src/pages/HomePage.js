import { Container, Fab } from '@material-ui/core';
import Header from '../components/Header';
import PostList from '../components/PostList';
import CreatePostModel from '../components/CreatePostModel';
import AddIcon from '@material-ui/icons/Add';
import useStyles from './styles'
import { useCallback } from 'react';
import { useDispatch } from 'react-redux';
import { showModal } from '../redux/actions';

const HomePage = () => {
    const classes = useStyles();
    const dispatch = useDispatch();

    const openCreatePostModal = useCallback(() => {
        dispatch(showModal())
    }, [dispatch]);

    return (
    <Container maxWidth="lg" className={{}}>
        <Header />
        <PostList />
        <CreatePostModel />
        <Fab className={classes.fab} color='primary' onClick={openCreatePostModal}>
            <AddIcon />
        </Fab>
    </Container>
    )
}

export default HomePage
