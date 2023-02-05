import {React, useState, useEffect} from 'react';
import { Card, CardBody, CardFooter, Stack, Heading, Text, Button  } from '@chakra-ui/react'
import FilterButton from '../FilterButton/FilterButton';
import GenerateButton from '../GenerateButton/GenerateButton';
import "./Recipe.css"

const Recipe = () => {
    const [recipes, setRecipes] = useState([]);

    const fetchRecipes = async () => {
        const response = await fetch("http://localhost:8000/recipes");
        const recipes = await response.json();
        setRecipes(recipes.data);
        console.log(recipes);
    }

    const renderRecipes = recipes => {
        console.log("see below");
        console.log(recipes);
        const rows = recipes.map((recipe, i) => (
            <div className="recipeBlock" variant='outline' key={i}>
            <CardBody>
            <h1 className="recipeTitle"><a href={recipe.link}>{recipe.title}</a></h1>
            <div className="recipeTimes">
                <p>Prep Time: {recipe.prep_time}</p>
                <p>Cook Time: {recipe.cook_time}</p>
                <p>Total Time: {recipe.total_time}</p>
            </div>
            <div className="portions">
              <p>Portions: {recipe.portions}</p>
            </div>
            <p className="recipeNutritionFacts">Nutrition Facts: {recipe.nutrition_facts}</p>
            </CardBody>
            <CardFooter>
            </CardFooter>
            </div>
        ));
        return rows;
      };
    
      useEffect(() => {
        fetchRecipes();
      }, []);
    

    return (
        <div className="recipeBox">
            <div className="recipeHeaderText">
                <h1>Try these recipes...</h1> 
                {/* <div className="filterButtonBox">
                <FilterButton/>
                </div> 
                <div className="generateButtonBox">
                <GenerateButton/>
                </div>   */}
            </div>
            <div className="recipeContainer">
        <Card
        direction={{ base: 'column', sm: 'row' }}
        overflow='hidden'
        variant='outline'
        >

        <Stack>{renderRecipes(recipes)}</Stack>
        
        </Card>
        </div>
        </div>
    );
};

export default Recipe;