import { INIT_STATE } from "../../constant";
import { getType, showModal, hideModal } from "../actions";

export default function modalReducer(state = INIT_STATE.modal, action) {
    switch(action.type) {
        case getType(showModal):// case 'getPostsRequest':
            return {
                isShow: true
            }
        case getType(hideModal):
            return {
                isShow: false
            }
        default:
            return state;
    }
}