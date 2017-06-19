
package us.kbase.kbparallel;

import java.util.HashMap;
import java.util.Map;
import javax.annotation.Generated;
import com.fasterxml.jackson.annotation.JsonAnyGetter;
import com.fasterxml.jackson.annotation.JsonAnySetter;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonPropertyOrder;
import us.kbase.common.service.UObject;


/**
 * <p>Original spec-file type: Task</p>
 * 
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "function",
    "params",
    "run_local"
})
public class Task {

    /**
     * <p>Original spec-file type: Function</p>
     * 
     * 
     */
    @JsonProperty("function")
    private Function function;
    @JsonProperty("params")
    private UObject params;
    @JsonProperty("run_local")
    private Long runLocal;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    /**
     * <p>Original spec-file type: Function</p>
     * 
     * 
     */
    @JsonProperty("function")
    public Function getFunction() {
        return function;
    }

    /**
     * <p>Original spec-file type: Function</p>
     * 
     * 
     */
    @JsonProperty("function")
    public void setFunction(Function function) {
        this.function = function;
    }

    public Task withFunction(Function function) {
        this.function = function;
        return this;
    }

    @JsonProperty("params")
    public UObject getParams() {
        return params;
    }

    @JsonProperty("params")
    public void setParams(UObject params) {
        this.params = params;
    }

    public Task withParams(UObject params) {
        this.params = params;
        return this;
    }

    @JsonProperty("run_local")
    public Long getRunLocal() {
        return runLocal;
    }

    @JsonProperty("run_local")
    public void setRunLocal(Long runLocal) {
        this.runLocal = runLocal;
    }

    public Task withRunLocal(Long runLocal) {
        this.runLocal = runLocal;
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
        return ((((((((("Task"+" [function=")+ function)+", params=")+ params)+", runLocal=")+ runLocal)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
