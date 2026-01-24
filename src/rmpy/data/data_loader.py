import polars as pl
from pathlib import Path

class DataLoader:

    REQUIRED_COLUMNS = {"booking_date", "departure_date", "itinerary_id", "seats_sold", "revenue"} #check this later

    @staticmethod
    def load_history(self, filepath: str):
        path = Path(filepath)

        if path.suffix == '.parquet':
            lf = pl.scan_parquet(path)
        else:
            lf = pl.scan_csv(path)
    
        columns = set(lf.columns)

        missing = DataLoader.REQUIRED_COLUMNS - columns
        if missing:
            raise ValueError(f"Data is missing to create itineraries {missing}")
        
        lf = lf.with_columns(
            [pl.col("booking_date").str.to_date(),
            pl.col("departure_date").str.to_date()]
            .with_columns(
            (pl.col('departure_date') - pl.col("booking_date")).dt.total_days().alias('dba')
            )
        )
        
        return lf.collect()