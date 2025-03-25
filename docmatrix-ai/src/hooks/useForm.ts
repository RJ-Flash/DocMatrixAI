import { useState, useCallback } from 'react';

interface ValidationRules {
  [key: string]: {
    required?: boolean;
    pattern?: RegExp;
    minLength?: number;
    maxLength?: number;
    validate?: (value: any) => boolean | string;
  };
}

interface ValidationErrors {
  [key: string]: string;
}

export function useForm<T extends { [key: string]: any }>(
  initialValues: T,
  validationRules?: ValidationRules,
  onSubmit?: (values: T) => void | Promise<void>
) {
  const [values, setValues] = useState<T>(initialValues);
  const [errors, setErrors] = useState<ValidationErrors>({});
  const [isSubmitting, setIsSubmitting] = useState(false);

  const validateField = useCallback(
    (name: string, value: any) => {
      if (!validationRules || !validationRules[name]) return '';

      const rules = validationRules[name];

      if (rules.required && !value) {
        return 'This field is required';
      }

      if (rules.pattern && !rules.pattern.test(value)) {
        return 'Invalid format';
      }

      if (rules.minLength && value.length < rules.minLength) {
        return `Minimum length is ${rules.minLength} characters`;
      }

      if (rules.maxLength && value.length > rules.maxLength) {
        return `Maximum length is ${rules.maxLength} characters`;
      }

      if (rules.validate) {
        const result = rules.validate(value);
        if (typeof result === 'string') return result;
        if (!result) return 'Invalid value';
      }

      return '';
    },
    [validationRules]
  );

  const handleChange = useCallback(
    (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
      const { name, value, type } = e.target;
      const newValue = type === 'checkbox' ? (e.target as HTMLInputElement).checked : value;

      setValues((prev) => ({ ...prev, [name]: newValue }));

      if (validationRules) {
        const error = validateField(name, newValue);
        setErrors((prev) => ({ ...prev, [name]: error }));
      }
    },
    [validateField, validationRules]
  );

  const handleSubmit = useCallback(
    async (e: React.FormEvent) => {
      e.preventDefault();
      
      if (!validationRules || !onSubmit) return;

      // Validate all fields
      const newErrors: ValidationErrors = {};
      let hasErrors = false;

      Object.keys(validationRules).forEach((key) => {
        const error = validateField(key, values[key]);
        if (error) {
          newErrors[key] = error;
          hasErrors = true;
        }
      });

      setErrors(newErrors);

      if (!hasErrors) {
        setIsSubmitting(true);
        try {
          await onSubmit(values);
        } catch (error) {
          console.error('Form submission error:', error);
        } finally {
          setIsSubmitting(false);
        }
      }
    },
    [values, validationRules, validateField, onSubmit]
  );

  const reset = useCallback(() => {
    setValues(initialValues);
    setErrors({});
    setIsSubmitting(false);
  }, [initialValues]);

  return {
    values,
    errors,
    isSubmitting,
    handleChange,
    handleSubmit,
    reset,
    setValues,
  };
} 