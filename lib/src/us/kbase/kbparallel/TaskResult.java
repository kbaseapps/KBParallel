
package us.kbase.kbparallel;

import java.util.HashMap;
import java.util.Map;
import javax.annotation.Generated;
import com.fasterxml.jackson.annotation.JsonAnyGetter;
import com.fasterxml.jackson.annotation.JsonAnySetter;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonPropertyOrder;


/**
 * <p>Original spec-file type: TaskResult</p>
 * 
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "is_error",
    "result_package"
})
public class TaskResult {

    @JsonProperty("is_error")
    private Long isError;
    /**
     * <p>Original spec-file type: ResultPackage</p>
     * 
     * 
     */
    @JsonProperty("result_package")
    private ResultPackage resultPackage;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("is_error")
    public Long getIsError() {
        return isError;
    }

    @JsonProperty("is_error")
    public void setIsError(Long isError) {
        this.isError = isError;
    }

    public TaskResult withIsError(Long isError) {
        this.isError = isError;
        return this;
    }

    /**
     * <p>Original spec-file type: ResultPackage</p>
     * 
     * 
     */
    @JsonProperty("result_package")
    public ResultPackage getResultPackage() {
        return resultPackage;
    }

    /**
     * <p>Original spec-file type: ResultPackage</p>
     * 
     * 
     */
    @JsonProperty("result_package")
    public void setResultPackage(ResultPackage resultPackage) {
        this.resultPackage = resultPackage;
    }

    public TaskResult withResultPackage(ResultPackage resultPackage) {
        this.resultPackage = resultPackage;
        return this;
    }

    @JsonAnyGetter
    public Map<String, Object> getAdditionalProperties() {
        return this.additionalProperties;
    }

    @JsonAnySetter
    public void setAdditionalProperties(String name, Object value) {
        this.additionalProperties.put(name, value);
    }

    @Override
    public String toString() {
        return ((((((("TaskResult"+" [isError=")+ isError)+", resultPackage=")+ resultPackage)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
