import mongoose from 'mongoose';

const schema = new mongoose.Schema({
    title: {
        type: String,
        required: true,
    },
    content: {
        type: String,
        required: true,
    },
    author: {
        type: String,
        required: true,
        default: 'Anonymus'
    },
    attachment: String,
    likeCount: {
        type: Number,
        default: 0,
    },
    comments: {
        type: Array,
        items: {
            type: Object,
            properties: {
                userComment: {
                    type: String,
                    required: true,
                },
                comment: {
                    type: String,
                    required: true,
                }
            }
        }
    }
}, {timestamps: true});

export const PostModel = mongoose.model('Post', schema)