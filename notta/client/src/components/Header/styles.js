import { makeStyles } from '@mui/styles';

export const useStyles = makeStyles((theme) => ({
    container: {
        display: 'flex',
        height: '50px', 
        alignItems: 'center', 
        backgroundColor: '#34568B',
    },
    drawer: {
        marginLeft: '5%',
        backgroundColor: 'white',
        minWidth: '100px',
        color: '#34568B',
        height: '30px',
    },
    mainText: {
        fontSize: '30px', 
        flexGrow: 1,
        color: 'white'
    },
    logInButton: {
        height: '30px', 
        marginRight: '5%',
        backgroundColor: 'white',
        minWidth: '100px',
        color: '#34568B',
    }
}))