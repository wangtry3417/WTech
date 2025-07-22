public class Test() {
   public static void main(String args[]) {
     // 可調用mapToJson函數
   }
   /**
     * 手動將 Map 轉換為 JSON 字符串（基本實現）
     * 支援 String, Number, Boolean, null, Map, Array
     */
    public static String mapToJson(Map<String, Object> map) {
        if (map == null) {
            return "null";
        }

        StringBuilder jsonBuilder = new StringBuilder();
        jsonBuilder.append("{");

        boolean firstEntry = true;
        for (Map.Entry<String, Object> entry : map.entrySet()) {
            if (!firstEntry) {
                jsonBuilder.append(",");
            }
            firstEntry = false;

            jsonBuilder.append("\"").append(escapeJson(entry.getKey())).append("\":");
            jsonBuilder.append(valueToJson(entry.getValue()));
        }

        jsonBuilder.append("}");
        return jsonBuilder.toString();
    }

    /**
     * 將任意 Java 值轉換為 JSON 字符串
     */
    private static String valueToJson(Object value) {
        if (value == null) {
            return "null";
        } else if (value instanceof String) {
            return "\"" + escapeJson((String) value) + "\"";
        } else if (value instanceof Number || value instanceof Boolean) {
            return value.toString();
        } else if (value instanceof Map) {
            @SuppressWarnings("unchecked")
            Map<String, Object> map = (Map<String, Object>) value;
            return mapToJson(map);
        } else if (value.getClass().isArray()) {
            return arrayToJson(value);
        } else {
            // 其他類型直接調用 toString()（可能不符合嚴格 JSON 規範）
            return "\"" + escapeJson(value.toString()) + "\"";
        }
    }

    /**
     * 將數組轉換為 JSON 數組字符串
     */
    private static String arrayToJson(Object array) {
        if (array == null) {
            return "null";
        }

        StringBuilder jsonBuilder = new StringBuilder();
        jsonBuilder.append("[");

        int length = java.lang.reflect.Array.getLength(array);
        for (int i = 0; i < length; i++) {
            if (i > 0) {
                jsonBuilder.append(",");
            }
            Object element = java.lang.reflect.Array.get(array, i);
            jsonBuilder.append(valueToJson(element));
        }

        jsonBuilder.append("]");
        return jsonBuilder.toString();
    }

    /**
     * 轉義 JSON 特殊字符
     */
    private static String escapeJson(String str) {
        if (str == null) {
            return "";
        }
        return str.replace("\\", "\\\\")
                  .replace("\"", "\\\"")
                  .replace("\b", "\\b")
                  .replace("\f", "\\f")
                  .replace("\n", "\\n")
                  .replace("\r", "\\r")
                  .replace("\t", "\\t");
    }
}