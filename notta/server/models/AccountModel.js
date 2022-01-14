import mongoose from 'mongoose';

const schema = new mongoose.Schema({
    name: {
        type: String,
        required: true,
    },
    password: {
        type: String,
        required: true,
    },
    userName: {
        type: String,
        required: true,
        default: 'Anonymous'
    },
    attachment: String
}, { timestamps: true });

export const AccountModel = mongoose.model('Account', schema);