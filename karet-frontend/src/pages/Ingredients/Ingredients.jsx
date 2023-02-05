import { React, useState, useEffect} from 'react';
import {
  Table,
  Thead,
  Tbody,
  Tfoot,
  Tr,
  Th,
  Td,
  TableCaption,
  TableContainer,
} from '@chakra-ui/react'
import AddIngredientButton from '../../components/AddIngredientButton/AddIngredientButton';

import './Ingredients.css';

const Ingredients = () => {
  const [ingredients, setIngredients] = useState([]);

  const fetchIngredients = async () => {
    const response = await fetch("http://localhost:8000/ingredients")
    const ingredients = await response.json()
    setIngredients(ingredients.data)
  }

  const renderIngredientRows = ingredients => {
    console.log(ingredients);
    const rows = ingredients.map((ingredient, i) => (
      <Tr key={i}>
        <Th>{ingredient[0]}</Th>
        <Th>{ingredient[1]}</Th>
        <Th>{ingredient[2]}</Th>
      </Tr>
    ));
    return rows;
  };

  useEffect(() => {
    fetchIngredients();
  }, []);

  return (
    <div className="ingredientsPage">
      <div className="ingredientHeader">
        <h1 className="title">List of Ingredients</h1>
        <div className="addButton">
        <AddIngredientButton />
        </div>
      </div>
      <TableContainer>
  <Table variant='simple'>
    <Thead>
      <Tr>
        <Th>Name</Th>
        <Th>Expiration date</Th>
        <Th>Location</Th>
      </Tr>
    </Thead>
    <Tbody>
      {renderIngredientRows(ingredients)}
    </Tbody>
    <Tfoot>
      <Tr>
      </Tr>
    </Tfoot>
  </Table>
</TableContainer>
    </div>
  );
};

export default Ingredients;
