## 設計模式與SOLID原則

### 1. 策略模式

採用策略模式來封裝不同的驗證與轉換策略，這樣可以在運行時自由選擇和替換算法，且提升擴充性。

- **驗證策略**：
  - `OrderFieldValidationStrategy`: 驗證訂單的必填欄位與資料類型。
  - `NameValidationStrategy`: 驗證名稱格式。
  - `PriceValidationStrategy`: 驗證價格是否超過限制。
  - `CurrencyValidationStrategy`: 驗證允許的貨幣類型。

- **轉換策略**：
  - `USDToTWDConversionStrategy`: 將價格從 USD 轉換為 TWD。
  - `NoConversionStrategy`: 不進行任何轉換。

### 2. SOLID 

#### 1. 單一職責原則 S

  - 每個策略類別只有一個責任
  -  `OrderValidator`：負責處理訂單的驗證邏輯，確保訂單的各個欄位符合要求。
  -  `OrderConverter`：專注於訂單的轉換邏輯，將訂單價格和幣種進行轉換。
    
#### 2. 開放封閉原則 O

  - 當之後需要新增name長度檢查策略，我只需新增一個類別 `NameLengthValidationStrategy`，將驗證策略添加到驗證列表中，而不改變現有代碼

#### 3. 里氏替換原則 L

  -  當我在 `OrderConverter` 中使用  `ConversionStrategy ` 類型的 strategy 時，可以用任意子類別替代。
  -  例如，新增一個RMB轉換策略，將 strategy 設置為  `RMBToTWDConversionStrategy `仍可正常使用。

#### 4. 介面隔離原則 I

  - 每個驗證及轉換策略類別，都實現了父類別的`validate` or `convert` 方法，並處理各自的驗證邏輯不被迫去實現無關聯的方法。

#### 5. 依賴反轉原則 D

  - `OrderValidator` 和 `OrderConverter` 依賴於 `ValidationStrategy` 和 `ConversionStrategy` 的抽象接口，而不是具體的實作類別。這樣可以隨意替換策略，保持高層模組與具體實作的解耦。
