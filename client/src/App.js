import React from 'react';
import {
  ChakraProvider,
  Box,
  Text,
  Link,
  VStack,
  Code,
  Grid,
  theme,
} from '@chakra-ui/react';
import { ColorModeSwitcher } from './ColorModeSwitcher';
import { Logo } from './Logo';
import {useState, useEffect} from 'react'

function App() {
  // store data from backend in data
  const [data, setData] = useState([{}]);

  // fetch members from backend to frontend, should re-render
  useEffect(() => {
    fetch('/members')
      .then(res => res.json())
      .then(data => {
        // call setData
        setData(data);
        console.log(data);
      });
  }, []);

  return (
    <ChakraProvider theme={theme}>
      <div>
        {typeof data.members === 'undefined' ? (
          <p>Loading...</p>
        ) : (
          data.members.map((member, i) => <p key={i}>{member}</p>)
        )}
      </div>
    </ChakraProvider>
  );
}

export default App;
