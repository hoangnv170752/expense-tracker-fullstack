import React, { useContext, useEffect, useState } from "react";
import { SimpleGrid, Text } from "@mantine/core";
import DisplayCard from "../components/DisplayCard";
import HistoryStack from "../components/HistoryStack";
import PageContainer from "../layout/PageContainer";
import PieChart from "../components/PieChart";
import CategoriesContext from "../store/CategoriesContext";

const HomePage = () => {
  const { getTotalAmount } = useContext(CategoriesContext);
  const budget = getTotalAmount("Budget");
  const expenses = getTotalAmount("Expenses");

  // State to store Bitcoin rates
  const [bitcoinRates, setBitcoinRates] = useState<{
    USD: number;
    EUR: number;
    VND: number;
  }>({
    USD: 0,
    EUR: 0,
    VND: 0,
  });

  // Fetch Bitcoin rates
  const fetchBitcoinRates = async () => {
    try {
      const response = await fetch("https://api.coindesk.com/v1/bpi/currentprice.json");
      const data = await response.json();
      const usdRate = data.bpi.USD.rate_float;
      const eurRate = data.bpi.EUR.rate_float;
      const vndRate = usdRate * 25380; // 1 USD = 25380 VND

      setBitcoinRates({
        USD: usdRate,
        EUR: eurRate,
        VND: vndRate,
      });
    } catch (error) {
      console.error("Error fetching Bitcoin rates:", error);
    }
  };

  useEffect(() => {
    fetchBitcoinRates();
  }, []);

  return (
    <PageContainer>
      <div
        style={{
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
        }}
      >
        <Text
          size={35}
          weight={700}
          mb={20}
          sx={(theme) => ({
            color:
              theme.colorScheme === "dark"
                ? theme.colors.dark[1]
                : theme.colors.gray[9],
          })}
        >
          YOUR BALANCE IS: ${budget - expenses}
        </Text>
        <Text
          size={15}
          weight={700}
          mb={20}
          sx={(theme) => ({
            color:
              theme.colorScheme === "dark"
                ? theme.colors.dark[1]
                : theme.colors.gray[9],
          })}
        >
          BITCOIN RATE:
          <br />
          USD: ${bitcoinRates.USD.toFixed(2)} <br />
          EUR: €{bitcoinRates.EUR.toFixed(2)} <br />
          VND: ₫{bitcoinRates.VND.toFixed(0)}
        </Text>
      </div>
      <SimpleGrid cols={2} style={{ justifyContent: "center" }}>
        <DisplayCard label="Income / Budget" amount={budget} color="green.4" />
        <DisplayCard label="Expenses" amount={expenses} color="red.4" />
        <HistoryStack />
        {(budget > 0 || expenses > 0) && <PieChart />}
      </SimpleGrid>
    </PageContainer>
  );
};

export default HomePage;