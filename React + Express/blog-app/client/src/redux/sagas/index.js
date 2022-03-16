import { takeLatest, call, put } from 'redux-saga/effects';
import * as actions from '../actions';
import * as api from '../../api'

function* fetchPostsSaga(action) {
    try {
        const posts = yield call(api.fetchPosts);
        // console.log(`[posts]`, posts);
        yield put(actions.getPosts.getPostsSuccess(posts.data)); 
    } catch(err) {
        console.log(err)
        yield put(actions.getPosts.getPostsFailure(err));
    }
    
};

function* createPostSaga(action) {
    try {
      const updatedPost = yield call(api.createPost, action.payload);
      yield put(actions.createPost.updatePostSuccess(updatedPost.data));
    } catch (err) {
      console.error(err);
      yield put(actions.createPost.updatePostFailure(err));
    }
  }

function* updatePostSaga(action) {
  try {
    const post = yield call(api.updatePost, action.payload);
    yield put(actions.updatePost.updatePostSuccess(post.data));
  } catch (err) {
    console.error(err);
    yield put(actions.updatePost.updatePostFailure(err));
  }
}
  

function* mySaga() {
    yield takeLatest(actions.getPosts.getPostsRequest,fetchPostsSaga);
    yield takeLatest(actions.createPost.createPostRequest,createPostSaga);
    yield takeLatest(actions.updatePost.updatePostRequest,updatePostSaga);
};

export default mySaga;