import {React, useState, useEffect} from "react";
import {
    Modal,
    ModalOverlay,
    ModalContent,
    ModalHeader,
    ModalFooter,
    ModalBody,
    ModalCloseButton,
    Button,
    FormControl,
    FormLabel,
    Input
  } from '@chakra-ui/react'
  import { useDisclosure } from '@chakra-ui/react'

import "./AddIngredientButton.css"

// const IngredientContext = React.createContext({
//     ingredients: [], fetchIngredients: () => {}
//   })

function AddIngredientButton() {
    const { isOpen, onOpen, onClose } = useDisclosure()
    
    const [name, setName] = useState('');
    const [expirationDate, setExpirationDate] = useState('');
    const [location, setLocation] = useState('');
    const [ingredients, setIngredients] = useState([]);

    //const {ingredient, fetchIngredient} = React.useContext(IngredientContext); 

    // const fetchIngredients = async () => {
    //     const response = await fetch("http://localhost:3001")
    //     const ingredients = await response.json()
    //     setIngredients(ingredients.data)
    // }
    // useEffect(() => {
    //     fetchIngredients()
    // }, [])
    

    const handleSubmit = (event) => {
        const newIngredient = {
            "name": name,
            "expirationDate": expirationDate,
            "location": location
        }

        fetch("http://localhost:8000/ingredients", {
            method: "POST",
            headers:  { "Content-Type": "application/json" },
            body: JSON.stringify(newIngredient)
        }).then(() => {console.log("sent request")})
        event.preventDefault();
    }

    return (
      <>
        <Button onClick={onOpen}>
            Add Ingredient
        </Button>
  
        <Modal
          isOpen={isOpen}
          onClose={onClose}
        >
          <ModalOverlay />
          <ModalContent>
            <ModalHeader>Ingredient Details</ModalHeader>
            <ModalCloseButton />
            <ModalBody pb={6}>
              <FormControl>
                <FormLabel>Ingredient name</FormLabel>
                <Input placeholder='ex. carrots' onChange={e => {setName(e.target.value);}}/>
              </FormControl>
  
              <FormControl mt={4}>
                <FormLabel>Expires on</FormLabel>
                <Input placeholder='MM/DD/YYYY' onChange={e => {setExpirationDate(e.target.value);}}/>
              </FormControl>

              <FormControl mt={4}>
                <FormLabel>Location</FormLabel>
                <Input placeholder='ex. freezer' onChange={e => {setLocation(e.target.value);}}/>
              </FormControl>
            </ModalBody>
  
            <ModalFooter>
              <Button colorScheme='blue' mr={3} onClick={handleSubmit}>
                Add
              </Button>
              <Button onClick={onClose}>Cancel</Button>
            </ModalFooter>
          </ModalContent>
        </Modal>
      </>
    )
  }

  export default AddIngredientButton;