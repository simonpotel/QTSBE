# Tests

Test suites and integration testing tools.

## Directory Structure

### /integrations
- `plotly_unit.sh` - Plotly visualization tests
- `strategy_viewer.sh` - Multi-symbol strategy testing

### /tools
- `data_fetch/` - Provider data fetching tests
- `fibonacci.py` - Fibonacci retracement testing

## Running Tests

### Plotly Tests
```bash
sh tests/integrations/plotly_unit.sh
```

### Strategy Tests
```bash
sh tests/integrations/strategy_viewer.sh
```

## Adding Tests

1. Create test file in appropriate directory
2. Update relevant README
3. Add to test suite if applicable