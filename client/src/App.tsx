import { Paper } from "@mantine/core";
import { MantineProvider } from "@mantine/core";
import MainAppShell from "./components/MainAppShell";
import { AvailableCategoriesContextProvider } from "./store/AvailableCategoriesContext";
import { CategoriesContextProvider } from "./store/CategoriesContext";
import { HistoryContextProvider } from "./store/HistoryContext";

export default function App() {
  return (
    <MantineProvider
      theme={{
        fontFamily: "open-sans",
        colorScheme: "dark",
        fontSizes: { md: 90 },
      }}
    >
      <Paper>
        <AvailableCategoriesContextProvider>
          <HistoryContextProvider>
            <CategoriesContextProvider>
              <MainAppShell />
            </CategoriesContextProvider>
          </HistoryContextProvider>
        </AvailableCategoriesContextProvider>
      </Paper>
    </MantineProvider>
  );
}
