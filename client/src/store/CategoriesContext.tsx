import { useLocalStorage } from "@mantine/hooks";
import { createContext, ReactNode, useContext } from "react";
import AvailableCategoriesContext from "./AvailableCategoriesContext";

type CategoriesContextProps = {
  children: ReactNode;
};

type Category = {
  label: string;
  id: string;
  amount: number;
};

type AvailableCategories = {
  label: string;
  value: string;
  isused: string;
};

type CategoriesContextType = {
  categories: Category[];
  getTotalAmount: (type: string) => number;
  resetAmount: (type: string) => void;
  setCategories: (categories: Category[]) => void;
  addCategory: (newCategory: Category) => void;
  deleteCategory: (label: string) => void;
  subtractCategoryAmount: (label: string, amount: number) => void;
};

const CategoriesContext = createContext<CategoriesContextType>({
  categories: [],
  getTotalAmount: (type: string) => {
    let total = 0;
    return total;
  },
  resetAmount: (type: string) => {},
  setCategories: (categories: Category[]) => {},
  addCategory: (newCategory: Category) => {},
  deleteCategory: (label: string) => {},
  subtractCategoryAmount: (label: string, amount: number) => {},
});

export function CategoriesContextProvider({
  children,
}: CategoriesContextProps) {
  const [categories, setCategories] = useLocalStorage<Category[]>({
    key: "categories",
    defaultValue: [],
  });
  const { setAvailableCategories } = useContext(AvailableCategoriesContext);

  function setCategoriesHandler(categories: Category[]) {
    setCategories(categories);
  }

  function getTotalAmount(type: string) {
    let total = 0;
    if (type === "Expenses") {
      categories.forEach((category) => {
        if (category.label !== "Budget") total += category.amount;
      });
    } else {
      categories.forEach((category) => {
        if (category.label === "Budget") total += category.amount;
      });
    }
    return total;
  }

  function resetAmount(type: string) {
    setCategories((prev) => {
      const arr: Category[] = JSON.parse(JSON.stringify(prev));
      const arr2: Category[] = [];
      arr.forEach((c) => {
        if (type === "Budget") {
          if (c.label !== "Budget") {
            arr2.push(c);
          }
        } else {
          if (c.label === "Budget") {
            arr2.push(c);
          }
        }
      });
      return arr2;
    });
  }

  function addCategoryHandler(newCategory: Category) {
    let arr: Category[] = [];
    let count = 0;
    setCategories((prev) => {
      arr = JSON.parse(JSON.stringify(prev));
      if (arr.length === 0) {
        return [newCategory];
      }
      arr = arr.map((c) => {
        if (c.label === newCategory.label) {
          c.amount += newCategory.amount;
          count++;
        }
        return c;
      });

      if (count === 0) {
        arr.push(newCategory);
      }
      return [...arr];
    });
  }

  function deleteCategory(label: string) {
    setCategories((prev) => {
      return prev.filter((cat) => cat.label !== label);
    });
  }

  function subtractCategoryAmount(label: string, amount: number) {
    setCategories((prev) => {
      const arr: Category[] = JSON.parse(JSON.stringify(prev));
      const arr2: Category[] = [];
      arr.forEach((c) => {
        if (c.label === label) {
          c.amount -= amount;
        }
        if (c.amount > 0) {
          arr2.push(c);
        } else {
          setAvailableCategories((prev) => {
            const arr3: AvailableCategories[] = JSON.parse(
              JSON.stringify(prev)
            );
            arr3.forEach((category) => {
              if (category.label === label) {
                category.isused = "false";
              }
            });
            return arr3;
          });
        }
      });
      return arr2;
    });
  }

  const context = {
    categories: categories,
    getTotalAmount: getTotalAmount,
    resetAmount: resetAmount,
    setCategories: setCategoriesHandler,
    addCategory: addCategoryHandler,
    deleteCategory: deleteCategory,
    subtractCategoryAmount: subtractCategoryAmount,
  };

  return (
    <CategoriesContext.Provider value={context}>
      {children}
    </CategoriesContext.Provider>
  );
}

export default CategoriesContext;
