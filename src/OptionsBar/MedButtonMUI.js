import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import Button from '@material-ui/core/Button';
import { sizing } from '@material-ui/system';


const useStyles = makeStyles((theme) => ({
  root: {
    '& > *': {
      margin: theme.spacing(1),
    },
  },
}));

export default function OutlinedButton() {
  const classes = useStyles();

  return (
    <div className={classes.root}>
      <Button variant="outlined"
              height = "90px"
        >Default</Button>
    </div>
  );
}
